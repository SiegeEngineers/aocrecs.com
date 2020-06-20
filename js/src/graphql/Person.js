import gql from 'graphql-tag'

import MatchFragment from '../graphql/MatchFragment.js'

export default gql`
query Person($id: Int!, $order: [String], $offset: Int!, $limit: Int!) {
  person(id: $id) {
    id
    name
    country
    first_name
    last_name
    age
    aoeelo_rank
    aoeelo_rate
    aoeelo_id
    esportsearnings_id
    earnings
    liquipedia
    portrait_link
    twitch
    mixer
    douyu
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
