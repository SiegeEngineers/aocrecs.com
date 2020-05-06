import gql from "graphql-tag"

export default gql`
  subscription {
    stats {
      match_count
      latest_summary {
        count
      }
    }
  }
`;
