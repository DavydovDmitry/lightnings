// Get identifier from location and use as gallery identifier
// to group images and videos with the same locations.
export function idFromLonLat(lon, lat){
  let precision = 2;
  let result = 'loc';
  [lat, lon].forEach((x) => {
      x = Number(x).toFixed(precision);
      result += String(x).replace('.', '');
  });
  return result;
}
