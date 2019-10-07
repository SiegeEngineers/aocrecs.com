import gql from 'graphql-tag';

import MatchFragment from "../graphql/MatchFragment.js"

export default gql`
query Civilization($id: Int!, $dataset_id: Int!, $offset: Int!, $limit: Int!) {
  civilization(id: $id, dataset_id: $dataset_id) {
    name
    bonuses {
      type
      description
    }
    matches(offset: $offset, limit: $limit) {
      count
      hits {
        ...MatchFragment
      }
    }
  }
}
${MatchFragment}
`
