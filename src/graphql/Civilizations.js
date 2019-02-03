import gql from 'graphql-tag';

export default gql`
query Civilizations($dataset_id: Int!) {
  stats {
    by_civilization(dataset_id: $dataset_id) {
      civilization {
        cid
        name
      }
      num_matches
      percent_matches
    }
  }
}
`
