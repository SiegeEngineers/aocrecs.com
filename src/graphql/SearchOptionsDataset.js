import gql from "graphql-tag";

export default gql`
query Stats($dataset_id: Int!)  {
    stats {
      civilizations(dataset_id: $dataset_id) { id label count }
    }
  }
`;
