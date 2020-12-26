import gql from 'graphql-tag';

export default gql`
query Ladders($platform_id: String!, $ladder_ids: [Int]) {
  meta_ladders(platform_id: $platform_id, ladder_ids: $ladder_ids) {
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
        person {
          id
          country
          name
        }
      }
    }
  }
}
`;
