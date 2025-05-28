"""
The documentation is mainly in english this code will be reused as a personal project
but the comments are left in swedish to explain the more complex stuff while english the general idea
"""

from typing import TypedDict
import torch
from torch.utils.data import Dataset
from pathlib import Path
from xml.etree import ElementTree as ET
from rdkit import Chem
from rdkit.Chem import rdmolops
from rdkit.Chem.rdchem import Atom, Bond
import numpy as np

DATA_PATH = Path(__file__).parent.parent / "dataset" / "2001" / "20010315.xml"


class ReactionSMILES(TypedDict):
    """
        TypedDict representing the extracted chemical reaction in SMILES format.

    Args:
        reactants (list[str]): List of SMILES strings for reactant molecules.
        products (list[str]): List of SMILES strings for product molecules.
    """

    reactants: list[str]
    products: list[str]


class ReactionSMILESArray(TypedDict):
    """
    TypedDict representing a chemical reaction where reactants and products
    are stored as arrays (e.g., molecular features or fingerprints).

    Attributes:
        reactants (list[np.ndarray]): List of NumPy arrays representing features of reactant molecules.
        products (list[np.ndarray]): List of NumPy arrays representing features of product molecules.
    """

    reactants: list[np.ndarray]
    products: list[np.ndarray]


class AtomFeatures(TypedDict):
    """Atom-level feature tensors exactly matching the dataset implementation.

    Attributes:
        node_product: torch.Tensor - Product atom features with shape [num_atoms, 5]
            Features in order:
                0: Atomic number (int)
                1: Degree (number of immediate neighbors)
                2: Total valence electrons (int)
                3: Formal charge (int)
                4: Number of explicit hydrogens (int)
        node_reactant: torch.Tensor - Reactant atom features with shape [num_atoms, 5]
            Same feature order as node_product"""

    node_product: torch.Tensor
    node_reactant: torch.Tensor


class EdgeFeatures(TypedDict):
    """
    Dictionary containing products and reactant edge feature i.e. explain the bonds between nodes.
    Formatted as tensor
    """

    prod_edge_feature: list[torch.Tensor]
    react_edge_feature: list[torch.Tensor]


class ReactionBatchData(TypedDict):
    """Dictionary containing

    Attributes:
        data: ReactionSMILESArray type
        node: AtomFeatures type
    """

    data: ReactionSMILESArray
    node: AtomFeatures
    edge_features: EdgeFeatures


class ChemicalReactionDataset(Dataset):
    """
    Dataset class for loading chemical reaction data from CML XML files.

    This dataset parses reactions into reactants and products represented as SMILES strings,
    suitable for training graph neural networks or other models.

    Args:
        data_path (Path | str): Path to the XML file containing reaction data.
            Defaults to a predefined dataset path.
    """

    def __init__(self, data_path: Path | str = DATA_PATH):
        """_summary_
            extract the data from
        Args:
            data_path (Path | str, optional): This is the xml path that you want to get data from. Defaults to DATA_PATH.
        """

        self._data_path = Path(data_path) if isinstance(data_path, str) else data_path

        if not self._data_path.exists():
            raise FileNotFoundError(f"Data file not found at: {data_path}")

        self.data = self._parse_reactions_smiles(self._data_path)
        self.prod_node, self.react_node = self._create_node(self.data)

        self.prod_edge_features, self.react_edge_features = self._create_edge_features(
            self.data
        )
        # for loop för ändra SMILE string till grannmatriser
        for idx, reaction in enumerate(self.data):
            product_arrs = []
            reactant_arrs = []

            # omvandla produkter till grann matriser
            for smile in reaction["products"]:
                mol = Chem.MolFromSmiles(smile)
                if mol is not None:
                    product_arrs.append(np.array(rdmolops.GetAdjacencyMatrix(mol)))

            # omvandla reaktanter till grann matriser
            for smile in reaction["reactants"]:
                mol = Chem.MolFromSmiles(smile)
                if mol is not None:
                    reactant_arrs.append(np.array(rdmolops.GetAdjacencyMatrix(mol)))

            self.data[idx] = {"products": product_arrs, "reactants": reactant_arrs}

    def __len__(self) -> int:
        """Return number of reactions in the dataset."""
        return len(self.data)

    def __getitem__(self, idx: int) -> ReactionBatchData:
        """Return node, edge features and the data itself in tensor/array format at specific index"""

        return {
            "data": self.data[idx],
            "node": {
                "node_product": self.prod_node[idx],
                "node_reactant": self.react_node[idx],
            },
            "edge_features": {
                "prod_edge_feature": self.prod_edge_features[idx],
                "react_edge_feature": self.react_edge_features[idx],
            },
        }

    def _parse_reactions_smiles(self, file_path: Path) -> list[ReactionSMILES]:
        """Parse CML XML file and extract reactants and products as SMILES strings.
            from the dataset
        Args:
            file_path (Path): Path to the CML XML file.

        Returns:
            list[ReactionSMILES]: List of reactions with reactants and products in SMILES.
        """
        # this function ONLY was created by chatgpt, because I couldn't afford to actually learn how to parse xml
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                xml_string = f.read()
        except Exception as e:
            raise RuntimeError(
                f"Failed to read file {file_path}: {str(e)}"
                + f"in {e.with_traceback()} "
            )

        root = ET.fromstring(xml_string)
        reactions = []
        # XML namespaces used in parsing the CML format
        namespaces = {
            "cml": "http://www.xml-cml.org/schema",
            "dl": "http://www.dl.org",
            "nameDict": "http://www.xml-cml.org/dictionary/cml/name/",
            "cmlDict": "http://www.xml-cml.org/dictionary/cml/",
            "unit": "http://www.xml-cml.org/unit/",
        }
        for reaction_elem in root.findall("cml:reaction", namespaces):
            reaction_data: ReactionSMILES = {
                "reactants": [],
                "products": [],
            }

            # Extrahera reaktanter
            for reactant in reaction_elem.findall(
                "cml:reactantList/cml:reactant", namespaces
            ):
                smiles_elem = reactant.find(
                    "cml:identifier[@dictRef='cml:smiles']", namespaces
                )
                if smiles_elem is not None:
                    smile = (
                        smiles_elem.attrib.get("value")
                        or (smiles_elem.text or "").strip()
                    )
                    if smile:
                        reaction_data["reactants"].append(smile)

            # Extrahera produkter
            for product in reaction_elem.findall(
                "cml:productList/cml:product", namespaces
            ):
                smiles_elem = product.find(
                    "cml:identifier[@dictRef='cml:smiles']", namespaces
                )
                if smiles_elem is not None:
                    smile = (
                        smiles_elem.attrib.get("value")
                        or (smiles_elem.text or "").strip()
                    )
                    if smile:
                        reaction_data["products"].append(smile)

            # Erhåller bara reaktioner med reaktanter och produkter
            if reaction_data["reactants"] and reaction_data["products"]:
                reactions.append(reaction_data)

        return reactions

    def _create_node(
        self, data: list[ReactionSMILES]
    ) -> tuple[torch.Tensor, torch.Tensor]:
        """
        This function creates the nodes of the molecules

        Args:
            data (list[ReactionSMILES]): list of SMILE string from the dataset

        Returns:
            tuple[torch.Tensor, torch.Tensor]: return a 3D temsor with the atom features for products and reactants
        """
        node_prod = []
        node_react = []

        for reaction in data:
            prod_atoms = []

            for smile in reaction["products"]:
                mol = Chem.MolFromSmiles(smile)
                atoms: list[Atom] = mol.GetAtoms()
                for atom in atoms:
                    prod_atoms.append(
                        [
                            atom.GetAtomicNum(),  # Grundämnesnummer
                            atom.GetDegree(),  # Antal bindningar
                            atom.GetTotalValence(),  # Total valenselektroner
                            atom.GetFormalCharge(),  # Formell laddning
                            atom.GetNumExplicitHs(),  # Antal explicita väteatomer
                        ]
                    )

            node_prod.append(torch.tensor(prod_atoms, dtype=torch.float))

            react_atoms = []

            for smile in reaction["reactants"]:
                mol = Chem.MolFromSmiles(smile)
                atoms: list[Atom] = mol.GetAtoms()
                for atom in atoms:
                    react_atoms.append(
                        [
                            atom.GetAtomicNum(),  # Grundämnesnummer
                            atom.GetDegree(),  # Antal bindningar
                            atom.GetTotalValence(),  # Total valenselektroner
                            atom.GetFormalCharge(),  # Formell laddning
                            atom.GetNumExplicitHs(),  # Antal väteatomer
                        ]
                    )
            node_react.append(torch.tensor(react_atoms, dtype=torch.float))

        # returnera en 3D matris som förklarar bindingar av molekyler
        return node_prod, node_react

    def _create_edge_features(
        self, data: list[ReactionSMILES]
    ) -> tuple[torch.Tensor, torch.Tensor]:
        """
        Create edge feature i.e. the connection between bonds in the molecule

        Returns:
            torch.Tensor of shape [num_bonds, num_edge_features]
        """
        prod_edge_features = []
        react_edge_features = []
        for reaction in data:
            for smile in reaction["products"]:
                mol = Chem.MolFromSmiles(smile)

                bonds: list[Bond] = mol.GetBonds()
                for bond in bonds:
                    prod_edge_features.append(
                        [
                            bond.GetBondTypeAsDouble(),  # returnerar bindningstyp i float
                            bond.GetIsConjugated(),  # returnera om det är
                            bond.IsInRing(),  # returnera om binding är i en ring struktur
                            bond.GetIsAromatic(),  # returner om det är aromatisk
                            # (OBS vet ej vad det är men kollat på nätet och handlar om form, så värt ta upp)
                        ]
                    )
            for smile in reaction["reactants"]:
                mol = Chem.MolFromSmiles(smile)

                bonds: list[Bond] = mol.GetBonds()
                for bond in bonds:
                    react_edge_features.append(
                        [
                            bond.GetBondTypeAsDouble(),  # returnerar bindningstyp i float
                            bond.GetIsConjugated(),  # returnera om det är
                            bond.IsInRing(),  # returnera om binding är i en ring struktur
                            bond.GetIsAromatic(),  # returner om det är aromatisk
                        ]
                    )
        prod_edge_features = torch.tensor(prod_edge_features, dtype=torch.float64)
        react_edge_features = torch.tensor(react_edge_features, dtype=torch.float64)

        return prod_edge_features, react_edge_features


# testa kod
if __name__ == "__main__":
    d = ChemicalReactionDataset()
    print(d[0])
