import gql from 'graphql-tag';

export default gql`
query Charts($match_id: Int!) {
  match(id: $match_id) {
    id
    players {
      name
      color_id
      user {
        id
        name
        platform_id
      }
      timeseries {
        timestamp_secs
        trade_profit
        tribute_sent
        tribute_received
      }
      trade_carts {
        timestamp_secs
        count
      }
      transactions {
        timestamp
        timestamp_secs
        sold_amount
        sold_resource
        bought_resource
      }
    }
    tribute {
      from_player {
        name
        color_id
        user {
          id
          name
          platform_id
        }
      }
      timestamp
      to_player {
        name
        color_id
        user {
          id
          name
          platform_id
        }
      }
      resource
      spent
      received
      fee
    }
    market {
      timestamp_secs
      sell_wood
      sell_food
      sell_stone
      buy_wood
      buy_food
      buy_stone
    }
  }
}
`
