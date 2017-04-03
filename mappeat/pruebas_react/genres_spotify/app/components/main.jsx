import React from 'react';
import ReactDOM from 'react-dom';


class Artist extends React.Component{
   constructor(props){
    	super(props);
    	this.state = {genres:[]};
    }
    
    componentWillMount(){
        fetch('https://api.spotify.com/v1/artists/3TVXtAsR1Inumwj472S9r4').then((response) => {return response.json();}).then((artist) => {this.setState({genres: artist["genres"]});
        
        console.log('->>genre',artist["genres"]);
                       })

    }
    
    render(){
        
        if(this.state.genres.length>0){
            return <ul>{this.state.genres.map(function(genre){
                return <li>{genre}</li>
            })}</ul>
        }
         else{
            return <h1>??</h1>
        }
    }
}
ReactDOM.render(<Artist />,document.getElementById('container')
);