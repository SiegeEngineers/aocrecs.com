import gql from 'graphql-tag';

export default gql`
query Flags($match_id: Int!) {
  match(id: $match_id) {
    id
    teams {
      winner
      players {
        color_id
        name
        user {
          id
          platform_id
          name
        }
        flags {
          type
          name
          count
          evidence {
            timestamp
            value
          }
        }
      }
    }
  }
}
`
