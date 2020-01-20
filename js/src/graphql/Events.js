import gql from 'graphql-tag';

export default gql`
{
  events {
    id
    year
    name
  }
}
`;
