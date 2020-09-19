export function idFromLonLat(lon, lat){
  let precision = 2;
  let result = 'loc';
  [lat, lon].forEach((x) => {
      x = Number(x).toFixed(precision);
      result += String(x).replace('.', '');
  });
  return result;
}
