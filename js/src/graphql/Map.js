import gql from 'graphql-tag';

import MatchFragment from '../graphql/MatchFragment.js'

export default gql`
query Map($name: String!, $offset: Int!, $limit: Int!) {
  map(name: $name) {
    name
    top_civilizations {
      id
      dataset_id
      name
    }
    preview_url
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
