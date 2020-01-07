import gql from "graphql-tag";

export default gql`
query Stats($platform_id: String!)  {
    search_options {
      ladders(platform_id: $platform_id) { value label }
    }
  }
`;
