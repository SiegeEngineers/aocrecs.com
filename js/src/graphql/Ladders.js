import gql from 'graphql-tag';

export default gql`
query Ladders($platform_id: String!) {
  meta_ladders(platform_id: $platform_id, ladder_ids: [131, 132]) {
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
          name
        }
      }
    }
  }
}
`;
