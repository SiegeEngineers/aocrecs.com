import gql from 'graphql-tag';

export default gql`
query Ladders($platform_id: String!) {
  meta_ladders(platform_id: $platform_id) {
    id
    platform_id
    name
    ranks(limit: 15) {
      rank
      rating
      user {
        id
        name
      }
    }
  }
}
`;
