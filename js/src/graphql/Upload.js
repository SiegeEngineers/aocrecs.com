import gql from 'graphql-tag'

export default gql`
  mutation($rec_file: Upload!) {
    upload(rec_file: $rec_file) {
      success
      message
      match_id
    }
  }
`
