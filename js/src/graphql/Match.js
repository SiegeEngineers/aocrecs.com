import gql from 'graphql-tag';

import MatchFragment from "../graphql/MatchFragment.js"

export default gql`
query Match($match_id: Int!) {
  match(id: $match_id) {
    ...MatchFragment
  }
}
${MatchFragment}
`
