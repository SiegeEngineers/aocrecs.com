import gql from "graphql-tag";

export default gql`
  {
    stats {
      files
      matches
      series
      users
      by_day {
        date
        matches
      }
      platforms { label count }
      encodings { label count }
      languages { label count }
      datasets { label count }
      diplomacy_types { label count }
      maps { label count }
      game_types { label count }
      speeds { label count }
    }
  }
`;
