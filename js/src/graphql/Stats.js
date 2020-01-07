import gql from "graphql-tag";

export default gql`
  {
    stats {
      match_count
      series_count
      player_count
      map_count
      by_day {
        date
        count
      }
      platforms { name count }
      languages { name count }
      datasets { name count }
      diplomacy { name count }
      types { name count }
    }
  }
`;
