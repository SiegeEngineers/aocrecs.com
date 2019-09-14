import gql from "graphql-tag";

export default gql`
  {
    stats {
      matches
      series
      users
      map_count
      by_day {
        date
        matches
      }
      platforms { id label count }
      languages { id label count }
      datasets { id label count }
      diplomacy_types { id label count }
      game_types { id label count }
    }
  }
`;
