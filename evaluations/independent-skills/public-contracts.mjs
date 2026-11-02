import assert from 'node:assert/strict';
import { pathToFileURL } from 'node:url';
class Element {
  constructor(tag) { this.tagName = tag; this.children = []; this.listeners = {}; this.textContent = ''; this.className = ''; }
  append(...nodes) { this.children.push(...nodes); }
  appendChild(node) { this.children.push(node); return node; }
  addEventListener(event, callback) { this.listeners[event] = callback; }
  click() { this.listeners.click?.(); }
}
globalThis.document = {createElement: tag => new Element(tag)};
const ui = await import(pathToFileURL(process.argv[2]));
const title = '<img src=x onerror=alert(1)>';
for (const [name, css] of [['productCard','card'],['compactProductCard','card card--compact']]) {
  const events=[];
  const card=ui[name]({id:17,title},(...args)=>events.push(args));
  assert.equal(card.tagName,'article'); assert.equal(card.className,css);
  assert.equal(card.children[0].tagName,'h2'); assert.equal(card.children[0].textContent,title);
  assert.equal(card.children[1].textContent,'Add'); card.children[1].click();
  assert.deepEqual(events,[[17]]);
}
for (const [quantity, expected] of [[2,1],[0,0]]) {
  const events=[];
  const card=ui.cartCard({id:8,title,quantity},(...args)=>events.push(args));
  assert.equal(card.tagName,'article'); assert.equal(card.className,'card');
  assert.equal(card.children[0].textContent,title);
  assert.equal(card.children[1].textContent,'Remove one'); card.children[1].click();
  assert.deepEqual(events,[[8,expected]]);
}
console.log('Existing public DOM/event contracts: passed');
if (process.argv.includes('--build')) {
  assert.equal(typeof ui.productList,'function');
  const empty=ui.productList([],()=>{});
  assert.equal(empty.tagName,'section'); assert.equal(empty.children.length,1);
  assert.equal(empty.children[0].tagName,'p'); assert.equal(empty.children[0].textContent,'Chưa có sản phẩm');
  const events=[];
  const list=ui.productList([{id:1,title:'A'},{id:2,title:'B'}],(...args)=>events.push(args));
  assert.equal(list.tagName,'section'); assert.equal(list.children.length,2);
  assert.equal(list.children[0].tagName,'article'); assert.equal(list.children[1].children[0].textContent,'B');
  list.children[1].children[1].click(); assert.deepEqual(events,[[2]]);
  console.log('Product list feature contracts: passed');
}
