# Code for inserting entities and relationship into neo4j database
from neo4j import GraphDatabase

class DataLoad():
    def __init__(self,URI,AUTH):
        self.uri=URI
        self.auth=AUTH

    def add_relationship(self,tx, head, relationship_type, tail):
        # Convert relationship_type to uppercase
        relationship_type = relationship_type.upper()

        # Replace spaces with underscores in relationship_type
        relationship_type = relationship_type.replace(" ", "_")

        query = (
            f"MERGE (h:Entity {{name: $head}}) "
            f"MERGE (t:Entity {{name: $tail}}) "
            f"MERGE (h)-[:{relationship_type}]->(t)"
        )
        tx.run(query, head=head, tail=tail)


    def load_data(self,kb):
        """Pushing the data to the Neo4j Graph Database.
        """
        data = kb.relations
        with GraphDatabase.driver(self.uri, auth=self.auth) as driver:
            with driver.session() as session:
                for item in data:
                    head = item['head']
                    relationship_type = item['type']
                    tail = item['tail']

                    session.write_transaction(self.add_relationship, head, relationship_type, tail)

if __name__ == "__main__":
    URI = "neo4j+s://2b8d2138.databases.neo4j.io"  # Update with your Neo4j server URI
    AUTH = ("neo4j", "qktQ5EjmkdIH6_TgA3H9by9conZXX5DH67IBQotmKso")  # Update with your Neo4j credentials
    data_obj=DataLoad()
    data_obj.load_data()
