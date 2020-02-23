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
    report(year: Int!, month: Int!, platform_id: String!, limit: Int = 25): Report
    reports: [ReportOption]
    person(id: Int!): Person
    people: [Person]
}

type SearchResult {
    matches(params: Dict!, offset: Int = 0, limit: Int = 10): Hits
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
    ladders(platform_id: String!): [KeyValue]
}

type SearchOptionsGeneral {
    team_sizes: [KeyValue]
    diplomacy_types: [KeyValue]
    game_types: [KeyValue]
    mirror: [KeyValue]
    rated: [KeyValue]
    rms_zr: [KeyValue]
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
    count: Int!
}

type Map {
    builtin: Boolean!
    name: String!
    count: Int!
    percent: Float!
    events: [Event]
    preview_url: String
    matches(offset: Int = 0, limit: Int = 10): Hits
    top_civilizations(limit: Int = 3): [Civilization]
}

type Civilization {
    id: Int!
    dataset_id: Int!
    name: String!
    count: Int!
    percent: Float!
    bonuses: [CivilizationBonus]
    matches(offset: Int = 0, limit: Int = 10): Hits
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
    map_events: [Event]
    duration_secs: Int
    played: Datetime
    rated: Boolean
    diplomacy_type: String
    team_size: String
    cheats: Boolean
    population_limit: Int
    lock_teams: Boolean
    mirror: Boolean
    dataset_version: String
    version: String
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
}

type Timeseries {
    timestamp: Datetime
    food: Int!
    wood: Int!
    stone: Int!
    gold: Int!
    population: Int!
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
    finished: Datetime
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
    maps: [Map]
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
    matches(offset: Int = 0, limit: Int = 10): Hits
}

type Side {
    series_id: Int!
    name: String!
    score: Int!
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
    matches(offset: Int = 0, limit: Int = 10): Hits
    top_map: Map
    top_civilization: Civilization
    top_dataset: Dataset
}

type Person {
    id: Int!
    country: String
    name: String!
    match_count: Int!
    first_year: Int!
    last_year: Int!
    aliases: [String]
    accounts: [User]
    events: [Event]
    matches(offset: Int = 0, limit: Int = 10): Hits
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
