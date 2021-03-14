import _ from 'lodash';
import React, { Component, createRef } from 'react';
import ReactDOMServer from 'react-dom/server';
import { DataSet, Network } from "vis-network/standalone";
import List from '@material-ui/core/List';
import ListItem from '@material-ui/core/ListItem';
import ListItemText from '@material-ui/core/ListItemText';
import CircularProgress from '@material-ui/core/CircularProgress';

import { getArtistMovies } from '../http/data';

class ArtistsGraph extends Component {

  constructor(props) {
    super(props);
    this.network = {};
    this.appRef = createRef();

    this.state = {
      artists: props.artists,
      movies: [],
      data: { nodes: new DataSet([]), edges: new DataSet([]) },
      loading: false
    };
  }

  componentDidMount() {
    var options = {
      nodes: {
        borderWidth: 1,
        size: 50
      },
      edges: {
        color: "lightgray",
      },
      physics: false
    };
    this.network = new Network(this.appRef.current, this.state.data, options);
    this.network.on('click', (properties) => {
      if (properties.edges.length === 1 && properties.nodes.length === 0) {
        // This means we clicked on an edge
        const edge = this.state.data.edges.get(properties.edges)[0];
        this.updateEdgePopupHTML(edge, properties);
      } else {
        this.hideEdgePopupHTML();
      }
    });

  }

  async componentDidUpdate() {
    const previousArtists = this.state.artists;
    const currentArtists = this.props.artists;

    if (previousArtists.length !== currentArtists.length && !this.state.loading) {
      await this.addArtist(_.last(currentArtists));
    }
  }

  
  render() {
    const { loading } = this.state;

    return (
        <React.Fragment>
          <div style={{ width: '100%', height: 600, opacity:(loading ? 0.5 : 1) }} ref={this.appRef}></div>
          <CircularProgress style={{ position: 'relative', left: '50%', top: -300-25, display: (loading ? 'block' : 'none') }} color="inherit" size={50} />
          <div id="moviesPopup" className="menu" style={{ display: 'none' }}></div>
        </React.Fragment>
    );
  }

  addArtist = async (artist) => {
    this.setState({ loading: true });
    const previousArtists = this.state.artists;
    const currentData = this.state.data;
    const currentMovies = this.state.movies;
    
    currentData.nodes.add(this.buildNodeFromArtist(artist));
    
    const artistMovies = await getArtistMovies(artist.id);

    for (let movie of artistMovies) {
      let existingMovie = _.find(currentMovies, m => m.id === movie.id);
      if (existingMovie) {
        if (!existingMovie.artists.has(artist.id)) {
          for (let a of existingMovie.artists) {
            const edgeId = this.generateEdgeId(a, artist.id);
            const existingEdge = currentData.edges.get(edgeId);
            if (existingEdge) {
              existingEdge.movies.add(movie);
              existingEdge.value++;
              currentData.edges.remove(edgeId);
              currentData.edges.add(existingEdge);
            } else {
              currentData.edges.add({
                id: edgeId,
                from: artist.id,
                to: a,
                value: 1,
                movies: new Set([ movie ]),
                smooth: false
              });
            }
          }
          existingMovie.artists.add(artist.id);
        }
      } else {
        currentMovies.push({
          id: movie.id,
          image: movie.image,
          title: movie.title,
          artists: new Set([ artist.id ])
        });
      }
    }

    previousArtists.push(artist);
    this.setState({ artists: previousArtists, movies: currentMovies, data: currentData, loading: false });
  }

  generateEdgeId = (artistId1, artistId2) => {
    return [ artistId1, artistId2 ].sort().join('-');
  }

  buildNodeFromArtist = (artist) => {
    return {
      id: artist.id,
      shape: "circularImage",
      image: artist.image,
      brokenImage: 'https://imdb-api.com/images/original/nopicture.jpg'
    };
  }

  updateEdgePopupHTML = (edge, properties) => {
    const html = ReactDOMServer.renderToStaticMarkup(
      <List>
        {Array.from(edge.movies).map(m => (
          <ListItem key={m.id}>
            <ListItemText primary={m.title} />
          </ListItem>
        ))}
      </List>
    );
    const div = document.getElementById('moviesPopup');
    div.style.position = 'absolute';
    div.style.left = `${properties.event.center.x}px`;
    div.style.top = `${properties.event.center.y}px`;
    div.style.display = 'block';
    div.innerHTML = html;

    return div;
  }

  hideEdgePopupHTML = () => {
    const div = document.getElementById('moviesPopup');
    div.style.display = 'none';
  }
};

export default ArtistsGraph;