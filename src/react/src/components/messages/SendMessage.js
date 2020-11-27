import React, { Component } from 'react'
import axios from 'axios';
import './SendMessage.css'

class SendMessage extends Component {
    constructor() {
        super()
        this.state = {
            message:''
        }
        this.handleChange = this.handleChange.bind(this)
        this.handleSubmit = this.handleSubmit.bind(this)
    }

    handleChange(e) {
        this.setState({
            message: e.target.value
        })
    }

    handleSubmit(e) {
        e.preventDefault()
        axios.post('http://127.0.0.1:8103/api/db_send_message', {'username1': localStorage.getItem('username'), 'username2': localStorage.getItem('targetUser'), 'message': this.state.message})
        .then(res => {
        });
        this.setState({
            message:''
        })
    }

    render() {
        return (
            <div className='message-pos'>
                <form
                    onSubmit={this.handleSubmit}
                    className='send-message'>
                    <input
                        onChange={this.handleChange}
                        value={this.state.message}
                        placeholder='Enter your message'
                        type='text'/>
                </form>
            </div>
        )
    }

}

export default SendMessage