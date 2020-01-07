import gql from "graphql-tag";

export default gql`
query Stats($dataset_id: Int!)  {
    search_options {
      civilizations(dataset_id: $dataset_id) { value label }
    }
  }
`;
