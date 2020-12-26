"""GraphQL Schema."""

from ariadne import gql

TYPE_DEFS = gql("""
type Query {
    map(name: String!): Map
    maps: [Map]
    civilization(id: Int!, dataset_id: Int!): Civilization
    civilizations(dataset_id: Int!): [Civilization]
    stats: Stats
    match(id: Int!): Match
    search: SearchResult
    search_options: SearchOptions
    event(id: String!): Event
    events: [Event]
    series(id: String!): Series
    datasets: [Dataset]
    platforms: [Platform]
    meta_ladders(platform_id: String!, ladder_ids: [Int]): [Ladder]
    user(id: String!, platform_id: String!): User
    report(year: Int!, month: Int!, limit: Int = 25): Report
    reports: [ReportOption]
    person(id: Int!): Person
    people: [Person]
    latest: Latest
    latest_summary: [LatestSummary]
}

type Subscription {
    stats: LiveStats
}

type LiveStats {
    match_count: Int!
    latest_summary: [LatestSummary]
}

type Latest {
    matches(dataset_id: Int!, order: [String], offset: Int = 0, limit: Int = 10): Hits
}

type LatestSummary {
    dataset: Dataset
    version: String!
    count: Int!
}

type SearchResult {
    matches(params: Dict!, order: [String], offset: Int = 0, limit: Int = 10): Hits
}

type StatImprovement {
    user: User
    rank: Int!
    min_rate: Int!
    max_rate: Int!
    diff_rate: Int!
    count: Int!
    wins: Int!
    losses: Int!
}

type StatUser {
    user: User
    rank: Int!
    change: Int
    count: Int!
}

type StatMap {
    map: Map
    rank: Int!
    count: Int!
    percent: Float!
}

type Report {
    total_matches: Int!
    total_players: Int!
    most_matches: [StatUser]
    popular_maps: [StatMap]
    longest_matches: [Match]
    rankings(platform_id: String!, ladder_id: Int!, limit: Int = 25): [Rank]
    most_improvement(platform_id: String!, ladder_id: Int!, limit: Int = 25): [StatImprovement]
}

type ReportOption {
    year: Int!
    month: Int!
}

type Ladder {
    id: Int!
    platform_id: String!
    name: String!
    ranks(limit: Int = 5): [Rank]
}

type Rank {
    rank: Int!
    rating: Int!
    streak: Int
    change: Int
    platform_id: String!
    ladder_id: Int!
    ladder: Ladder
    user: User
    rate_by_day: [StatDate]
}

type Hits {
    count: Int!
    hits: [Match]
}

type Stats {
    match_count: Int!
    series_count: Int!
    player_count: Int!
    map_count: Int!
    datasets: [StatItem]
    platforms: [StatItem]
    diplomacy: [StatItem]
    languages: [StatItem]
    types: [StatItem]
    by_day: [StatDate]
}

type SearchOptions {
    general: SearchOptionsGeneral
    civilizations(dataset_id: Int!): [KeyValue]
    versions(dataset_id: Int!): [KeyValue]
    ladders(platform_id: String!): [KeyValue]
}

type SearchOptionsGeneral {
    team_sizes: [KeyValue]
    diplomacy_types: [KeyValue]
    game_types: [KeyValue]
    mirror: [KeyValue]
    rated: [KeyValue]
    rms_zr: [KeyValue]
    playback: [KeyValue]
    events: [KeyValue]
    tournaments: [KeyValue]
    winner: [KeyValue]
    mvp: [KeyValue]
    colors: [KeyValue]
    datasets: [KeyValue]
    platforms: [KeyValue]
    civilizations: [KeyValue]
    ladders: [KeyValue]
}

type KeyValue {
    value: String!
    label: String!
}

type StatItem {
    name: String!
    count: Int!
}

type StatDate {
    date: Datetime
    count: Int
}

type Map {
    builtin: Boolean!
    name: String!
    count: Int!
    percent: Float!
    events: [Event]
    preview_url: String
    matches(order: [String], offset: Int = 0, limit: Int = 10): Hits
    top_civilizations(limit: Int = 3): [Civilization]
}

type Civilization {
    id: Int!
    dataset_id: Int!
    name: String!
    count: Int!
    percent: Float!
    bonuses: [CivilizationBonus]
    matches(order: [String], offset: Int = 0, limit: Int = 10): Hits
}

type CivilizationBonus {
    type: String!
    description: String!
}

type File {
    id: Int!
    match_id: Int!
    original_filename: String!
    size: Int!
    language: String!
    encoding: String!
    owner: Player!
    download_link: String!
}

type Match {
    id: Int!
    map_name: String!
    rms_seed: Int
    rms_custom: Int
    guard_state: Boolean
    fixed_positions: Boolean
    direct_placement: Boolean
    effect_quantity: Boolean
    map_events: [Event]
    duration: Datetime
    duration_secs: Int
    played: Datetime
    added: Datetime
    has_playback: Boolean
    rated: Boolean
    diplomacy_type: String
    team_size: String
    cheats: Boolean
    population_limit: Int
    lock_teams: Boolean
    mirror: Boolean
    dataset_version: String
    version: String
    game_version: String
    save_version: String
    build: String
    postgame: Boolean
    platform_match_id: String
    winning_team_id: Int
    players: [Player]
    teams: [Team]
    winning_team: Team
    losing_team: Team
    chat: [Chat]
    files: [File]
    difficulty: String!
    type: String!
    map_size: String!
    map_reveal_choice: String!
    speed: String!
    starting_resources: String!
    starting_age: String!
    victory_condition: String!
    dataset: Dataset
    platform: Platform
    ladder: Ladder
    event: Event
    tournament: Tournament
    series: Series
    minimap_link: String!
    odds: Odds
    graph: Graph
    market: [MarketPrice]
    tribute: [Tribute]
}

type Tribute {
    timestamp: Datetime!
    timestamp_secs: Int!
    from_player: Player!
    to_player: Player!
    resource: String!
    spent: Int!
    received: Int!
    fee: Int!
}

type MarketPrice {
    timestamp: Datetime!
    timestamp_secs: Int!
    sell_food: Int!
    sell_wood: Int!
    sell_stone: Int!
    buy_food: Int!
    buy_wood: Int!
    buy_stone: Int!
}

type TrainedCount {
    player_number: Int!
    object_id: Int!
    timestamp_secs: Int!
    timestamp: Datetime!
    name: String!
    count: Int!
}

type Graph {
    nodes: [GraphNode]
    links: [GraphLink]
}

type GraphNode {
    id: Int!
    name: String!
    color_id: Int
}

type GraphLink {
    source: Int!
    target: Int!
}

type Odds {
    teams: [StatOdds]
    teams_and_civilizations: [StatOdds]
    civilizations: [StatOdds]
    civilizations_and_map: [StatOdds]
    teams_and_map: [StatOdds]
}

type StatOdds {
    wins: Int!
    losses: Int!
    percent: Float!
}

type Dataset {
    id: Int!
    name: String!
}

type Platform {
    id: String!
    name: String!
    url: String
    match_url: String
    ladders: [Ladder]
}

type Player {
    match_id: Int!
    team_id: Int!
    platform_id: String
    user: User
    number: Int!
    name: String!
    color: String!
    color_id: Int!
    winner: Boolean!
    rate_snapshot: Float
    rate_before: Float
    rate_after: Float
    mvp: Boolean
    human: Boolean
    score: Int
    military_score: Int
    economy_score: Int
    technology_score: Int
    society_score: Int
    units_killed: Int
    units_lost: Int
    buildings_razed: Int
    buildings_lost: Int
    units_converted: Int
    food_collected: Int
    wood_collected: Int
    stone_collected: Int
    gold_collected: Int
    tribute_sent: Int
    tribute_received: Int
    trade_gold: Int
    relic_gold: Int
    feudal_time: Datetime
    castle_time: Datetime
    imperial_time: Datetime
    feudal_time_secs: Int
    castle_time_secs: Int
    imperial_time_secs: Int
    explored_percent: Int
    research_count: Int
    total_wonders: Int
    total_castles: Int
    total_relics: Int
    villager_high: Int
    research: [Research]
    civilization: Civilization
    timeseries: [Timeseries]
    apm: [APM]
    map_control: [MapControl]
    units_trained: [TrainedCount]
    flags: [Flag]
    metrics: Metrics
    villager_allocation: [VillagerAllocation]
    trade_carts: [ObjectCount]
    villagers: [ObjectCount]
    transactions: [Transaction]
}

type Transaction {
    timestamp: Datetime!
    timestamp_secs: Int!
    sold_resource: String!
    sold_amount: Int!
    bought_resource: String!
    bought_amount: Int
}

type ObjectCount {
    timestamp: Datetime!
    timestamp_secs: Int!
    count: Int!
}

type MapControl {
    timestamp: Datetime!
    timestamp_secs: Int!
    control_percent: Int!
}

type APM {
    timestamp: Datetime!
    timestamp_secs: Int!
    actions: Int!
}

type VillagerAllocation {
    timestamp: Datetime!
    timestamp_secs: Int!
    name: String!
    count: Int!
}

type Metrics {
    total_tcs: Int!
    average_floating_resources: Int!
    dark_age_tc_idle: Datetime!
    seconds_housed: Datetime!
    seconds_villagers_idle: Datetime
    seconds_popcapped: Datetime!
}

type Flag {
    type: String!
    name: String!
    count: Int
    evidence: [Evidence]
}

type Evidence {
    timestamp: Datetime!
    value: String
}

type Timeseries {
    timestamp: Datetime
    timestamp_secs: Int!
    total_food: Int!
    total_wood: Int!
    total_stone: Int!
    total_gold: Int!
    population: Float!
    military: Float!
    percent_explored: Float!
    relic_gold: Int!
    trade_profit: Int!
    tribute_sent: Int!
    tribute_received: Int!
    value_current_buildings: Int!
    value_current_units: Int!
    value_lost_buildings: Int!
    value_lost_units: Int!
    value_objects_destroyed: Int!
    value_spent_objects: Int!
    value_spent_research: Int!
    roi: Float!
    damage: Float!
    kills: Int!
    deaths: Int!
    razes: Int!
    kd_delta: Int!
}

type Team {
    match_id: Int!
    team_id: Int!
    winner: Boolean!
    players: [Player]
}

type Research {
    id: Int!
    name: String!
    started: Datetime!
    started_secs: Int!
    finished: Datetime
    finished_secs: Int
}

type Chat {
    player: Player!
    message: String!
    audience: String!
    origination: String!
    timestamp: Datetime!
}

type Event {
    id: String!
    year: Int!
    name: String!
    tournaments: [Tournament]
    maps: [EventMap]
    players: [EventPlayer]
    civilizations: [EventCivilization]
}

type EventPlayer {
    player: Player!
    match_count: Int!
    win_percent: Float!
    average_duration: Datetime!
    most_played_civilization: Civilization!
    most_played_map: String!
}

type EventMap {
    map: Map!
    match_count: Int!
    played_percent: Float!
    average_duration: Datetime!
    most_played_civilization: Civilization!
}

type EventCivilization {
    civilization: Civilization!
    match_count: Int!
    win_percent: Float!
    average_duration: Datetime!
    most_played_map: String!
}

type Tournament {
    id: String!
    event_id: String!
    name: String!
    event: Event
    series: [Series]
}

type Series {
    id: String!
    tournament_id: Int!
    played: Datetime!
    name: String!
    sides: [Side]
    tournament: Tournament
    participants: [Participant]
    match_ids: [Int!]
    matches(order: [String], offset: Int = 0, limit: Int = 10): Hits
}

type Side {
    series_id: Int!
    name: String!
    score: Int
    winner: Boolean
    users: [User]
}

type Participant {
    series_id: Int!
    name: String
    score: Int
    winner: Boolean
}

type User {
    id: String!
    platform_id: String!
    platform: Platform
    name: String!
    person: Person
    meta_ranks(ladder_ids: [Int]): [Rank]
    matches(order: [String], offset: Int = 0, limit: Int = 10): Hits
    top_map: Map
    top_civilization: Civilization
    top_dataset: Dataset
}

type Person {
    id: Int!
    country: String
    name: String!
    first_name: String
    last_name: String
    birthday: Datetime
    age: Int
    earnings: Float
    esportsearnings_id: Int
    aoeelo_id: Int
    aoeelo_rank: Int
    aoeelo_rate: Int
    liquipedia: String
    portrait_link: String
    twitch: String
    mixer: String
    douyu: String
    youtube: String
    discord: String
    match_count: Int!
    first_year: Int!
    last_year: Int!
    aliases: [String]
    accounts: [User]
    events: [Event]
    matches(order: [String], offset: Int = 0, limit: Int = 10): Hits
}

type Mutation {
    upload(rec_file: Upload!): UploadResult!
}

type UploadResult {
    success: Boolean!
    message: String
    match_id: Int
}

scalar Datetime
scalar Dict
scalar Upload
""")
