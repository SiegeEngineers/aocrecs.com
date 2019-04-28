import gql from 'graphql-tag';

export default gql`
fragment MatchFragment on Match {
  id
  duration_secs
  played
  type {
    name
  }
  rated
  diplomacy_type
  team_size
  map_name
  platform_match_id
  cheats
  map_size {
    name
  }
  rms_seed
  hash
  map_reveal_choice {
    name
  }
  population_limit
  speed {
    name
  }
  lock_teams
  difficulty {
    name
  }
  mirror
  dataset {
    name
  }
  platform {
    id
    name
    url
    match_url
  }
  dataset_version
  ladder {
    lid
    platform_id
    name
  }
  series {
    id
    metadata {
      name
    }
  }
  tournament {
    id
    name
  }
  event {
    id
    name
  }
  version
  teams {
    winner
    members {
      name
      color_id
      user_id
      user {
        name
      }
      civilization {
        cid
        dataset_id
        name
      }
      rate_snapshot
      mvp
      human
      winner
      score
      rate_before
      rate_after
      military_score
      economy_score
      technology_score
      society_score
      units_killed
      hit_points_killed
      units_lost
      buildings_razed
      hit_points_razed
      buildings_lost
      units_converted
      food_collected
      wood_collected
      stone_collected
      gold_collected
      tribute_sent
      tribute_received
      trade_gold
      relic_gold
      feudal_time_secs
      castle_time_secs
      imperial_time_secs
      explored_percent
      research_count
      total_wonders
      total_castles
      total_relics
      villager_high
    }
  }
  files {
    id
    original_filename
    size
    compressed_size
    encoding
    language
    parser_version
    hash
    owner {
      name
    }
  }
}
`
