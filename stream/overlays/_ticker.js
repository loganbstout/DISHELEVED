/* Shared bottom-marquee builder for Disheveled stream overlays.
   Duplicates the item run so the -50% CSS translate loops seamlessly. */
function dshTicker(track, spec){
  if(!track) return;
  var items = (spec || 'Disheveled Studio|Collection 001|50 Units|No Restock|Messy By Design|Build In Public')
                .split('|').map(function(s){ return s.trim(); }).filter(Boolean);
  function run(){
    var el = document.createElement('div');
    el.className = 'mq-i';
    items.forEach(function(t){
      var s = document.createElement('span'); s.textContent = t; el.appendChild(s);
      var d = document.createElement('span'); d.className = 'mq-d'; el.appendChild(d);
    });
    return el;
  }
  track.textContent = '';
  track.appendChild(run());
  track.appendChild(run());
}
