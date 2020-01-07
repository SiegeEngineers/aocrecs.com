import gql from 'graphql-tag';

export default gql`
query Civilizations($dataset_id: Int!) {
  civilizations(dataset_id: $dataset_id) {
    id
    dataset_id
    name
    count
    percent
  }
}
`
