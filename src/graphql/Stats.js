import gql from "graphql-tag";

export default gql`
  {
    stats {
      files
      matches
      series
      voobly_users
      by_day {
        date
        matches
      }
    }
  }
`;
