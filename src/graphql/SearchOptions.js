import gql from "graphql-tag";

export default gql`
  {
    stats {
      platforms { id label count }
      datasets { id label count }
      team_sizes { id label count }
      diplomacy_types { id label count }
      maps { id label count }
      game_types { id label count }
      population_limits { id label count }
      events { id label count }
      tournaments { id label count }
      mirror { id label count }
      rated { id label count }
      rms_zr { id label count }
    }
  }
`;
