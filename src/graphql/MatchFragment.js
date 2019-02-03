import gql from 'graphql-tag';

export default gql`
fragment MatchFragment on Match {
  id
  duration_secs
  played
  type
  rated
  diplomacy_type
  team_size
  map {
    id
    name
  }
  voobly_id
  cheats
  map_size
  reveal_map
  population_limit
  speed
  lock_teams
  difficulty
  mirror
  dataset {
    name
  }
  dataset_version
  voobly_ladder {
    id
    name
  }
  series {
    name
  }
  version
  teams {
    winner
    members {
      name
      color_id
      voobly_user_id
      voobly_user {
        name
      }
      civilization {
        cid
        name
      }
      mvp
      human
      winner
      score
      rate_before
      rate_after
    }
  }
  files {
    id
    original_filename
    size
    owner {
      name
    }
  }
}
`
