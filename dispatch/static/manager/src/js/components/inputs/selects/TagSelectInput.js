import React from 'react'
import { connect } from 'react-redux'

import ItemSelectInput from './ItemSelectInput'

import tagsActions from '../../../actions/TagsActions'

class TagSelectInputComponent extends React.Component {

  listTags(query) {
    let queryObj = {}

    if (query) {
      queryObj['q'] = query
    }

    this.props.listTags(this.props.token, queryObj)
  }

  render() {
    return (
      <ItemSelectInput
        value={this.props.value}
        results={this.props.tags.ids}
        entities={this.props.entities.tags}
        onChange={(value) => this.props.update(value)}
        fetchResults={(query) => this.listTags(query)}
        create={(name, cb) => this.props.createTag(this.props.token, { name }, cb)}
        attribute='name'
        editMessage={this.props.value && this.props.value.length ? 'Edit tags' : 'Add tags'} />
    )
  }

}

const mapStateToProps = (state) => {
  return {
    tags: state.app.tags.list,
    entities: {
      tags: state.app.entities.tags
    },
    token: state.app.auth.token
  }
}

const mapDispatchToProps = (dispatch) => {
  return {
    listTags: (token, query) => {
      dispatch(tagsActions.list(token, query))
    },
    createTag: (token, data, callback) => {
      dispatch(tagsActions.create(token, data, null, callback))
    }
  }
}

const TagSelectInput = connect(
  mapStateToProps,
  mapDispatchToProps
)(TagSelectInputComponent)

export default TagSelectInput
