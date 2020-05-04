import gql from 'graphql-tag'

import MatchFragment from '../graphql/MatchFragment.js'

export default gql`
query Person($id: Int!, $offset: Int!, $limit: Int!) {
  person(id: $id) {
    id
    name
    country
    first_name
    last_name
    aoeelo_rank
    aoeelo_rate
    aoeelo_id
    esportsearnings_id
    earnings
    portrait_link
    twitch
    mixer
    youtube
    discord
    accounts {
      id
      name
      platform_id
      platform {
        id
        name
      }
    }
    events {
      id
      name
      year
    }
    aliases
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
