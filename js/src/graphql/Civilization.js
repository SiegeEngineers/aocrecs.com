import gql from 'graphql-tag';

import MatchFragment from "../graphql/MatchFragment.js"

export default gql`
query Civilization($id: Int!, $dataset_id: Int!, $order: [String], $offset: Int!, $limit: Int!) {
  civilization(id: $id, dataset_id: $dataset_id) {
    name
    bonuses {
      type
      description
    }
    matches(order: $order, offset: $offset, limit: $limit) {
      count
      hits {
        ...MatchFragment
      }
    }
  }
}
${MatchFragment}
`
