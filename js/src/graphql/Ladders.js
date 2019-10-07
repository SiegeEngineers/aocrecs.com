import gql from 'graphql-tag';

export default gql`
query Ladders($platform_id: String!) {
  meta_ladders(platform_id: $platform_id) {
    id
    platform_id
    name
    ranks(limit: 25) {
      rank
      rating
      streak
      user {
        id
        name
        canonical_name
      }
    }
  }
}
`;
