import React, { useEffect, useState, useCallback } from 'react';
import { makeStyles } from '@material-ui/core/styles';
import Grid from '@material-ui/core/Grid';

import ArtistSearch from './ArtistSearch';
import ArtistsGraph from './ArtistsGraph';

const styles = theme => ({
  container: {
    width: 800
  }
});

const ArtistsNetwork = () => {
  const classes = makeStyles(styles);

  const [ artists, setArtists ] = useState([]);

  const onArtistSelect = useCallback((artist) => {
    const newArtists = artists.concat([artist]);
    setArtists(newArtists);
  });

  return (
    <Grid container className={classes.container} >
      <Grid item style={{ width: '100%' }}>
        <ArtistSearch onArtistSelect={onArtistSelect} />
      </Grid>
      <Grid item style={{ width: '100%' }}>
        <ArtistsGraph artists={artists} />
      </Grid>
    </Grid>
  );
};

export default ArtistsNetwork;

