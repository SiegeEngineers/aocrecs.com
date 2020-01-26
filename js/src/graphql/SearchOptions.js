import gql from "graphql-tag";

export default gql`
  {
    search_options {
      general {
        platforms { value label }
        datasets { value label }
        team_sizes { value label }
        diplomacy_types { value label }
        game_types { value label }
        events { value label }
        tournaments { value label }
        mirror { value label }
        rated { value label }
        rms_zr { value label }
        playback { value label }
        colors { value label }
        winner { value label }
        mvp { value label }
      }
    }
  }
`;
