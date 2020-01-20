import gql from 'graphql-tag';

export default gql`
query Chat($match_id: Int!) {
  match(id: $match_id) {
    chat {
      audience
      origination
      timestamp
      message
      player {
        color_id
        name
      }
    }
  }
}
`
