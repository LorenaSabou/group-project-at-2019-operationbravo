import React from 'react';
import axios from 'axios';
import ReactTable from "react-table";
import "react-table/react-table.css";

class PageContent extends React.Component{


    constructor(props){
        super(props);
        this.state = {
            rooms : [
                {
                    roomId: 1,
                    roomName: "Edison",
                    num_persons: 5
                },
                {
                    roomId: 2,
                    roomName: "Newton",
                    num_persons: 7
                },
                {
                    roomId: 3,
                    roomName: "Babbage",
                    num_persons: 8
                },
                {
                    roomId: 4,
                    roomName: "Tesla",
                    num_persons: 4
                }
            ]
        };
        this.recheck = this.recheck.bind(this);
    }

    componentDidMount() {
        axios.get('https://reqres.in/api/users?page=2')
            .then(res => {
                const num_persons = res.data.total;
                this.setState({ num_persons: num_persons });
            })
    }

    findPositionById(roomId) {
        return this.state.rooms.findIndex(x => x.roomId == roomId);
    }

    recheck(roomId){
        const pos = this.findPositionById(roomId);
        this.setState(oldState => {
            let rooms = oldState.rooms.slice();
            let copy = Object.assign({}, rooms[pos]);
            copy.num_persons+=1;

            rooms[pos] = copy;

            return {
                rooms: rooms
            };
        });
    }



    render(){

        const columns = [
            {
                Header: "Room Id",
                accessor: "roomId",
                style: {
                    textAlign: "center"
                }
            },
            {
                Header: "Room Name",
                accessor: "roomName",
                style: {
                    textAlign: "center"
                }
            },
            {
                Header: "Number of Persons",
                accessor: "num_persons",
                style: {
                    textAlign: "center"
                }
            },
            {
                Header: "Action",
                Cell: props =>{
                    return (<button type="button"
                                    onClick={() => {
                                           this.recheck(props.original.roomId)
                                        }}>Recheck</button>)
                },
                style: {
                    textAlign: "center"
                }

            },
        ];

        const data = this.state.rooms;

        return <div>
            <ReactTable
                columns = {columns}
                data={data}
                showPagination={false}
                defaultPageSize={this.state.rooms.length}>
            </ReactTable>
        </div>
    }
}


export default PageContent;
