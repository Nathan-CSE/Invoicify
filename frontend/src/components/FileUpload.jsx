import React, { Component } from "react";
import { DropzoneArea } from "mui-file-dropzone";
import '../FileUploadStyles.css';
// See https://yuvaleros.github.io/material-ui-dropzone/ for documentation

class FileUpload extends Component {
  constructor(props) {
    super(props);
    this.state = {
      files: [],
    };
  }

  handleChange(files) {
    this.setState({
      files: files,
    });

    console.log('files: ', files);
  }
  render() {
    return (
      <DropzoneArea
        onChange={this.handleChange.bind(this)}
        dropzoneText='Upload Invoice(s): CSV, Excel, SQL, PDF'
        dropzoneClass="FileUploadClass"
        dropzoneParagraphClass="FileUploadTextClass"
      />
    );
  }
}

export default FileUpload;