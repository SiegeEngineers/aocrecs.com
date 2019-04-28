import gql from "graphql-tag";

export default gql`
query Stats($platform_id: String!)  {
    stats {
      ladders(platform_id: $platform_id) { id label count }
    }
  }
`;
