import gql from 'graphql-tag';

export default gql`
query Graph($match_id: Int!) {
  match(id: $match_id) {
    id
    graph {
      nodes {
        id
        name
      }
      links {
        source
        target
      }
    }
  }
}
`
