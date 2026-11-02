import { nextQuantity } from './cart.js';

export function productCard(product, onAdd) {
  const card = document.createElement('article');
  card.className = 'card';
  const title = document.createElement('h2');
  title.textContent = product.title;
  const button = document.createElement('button');
  button.textContent = 'Add';
  button.addEventListener('click', () => onAdd(product.id));
  card.append(title, button);
  return card;
}

export function cartCard(item, onQuantity) {
  const card = document.createElement('article');
  card.className = 'card';
  const title = document.createElement('h2');
  title.textContent = item.title;
  const button = document.createElement('button');
  button.textContent = 'Remove one';
  button.addEventListener('click', () => onQuantity(item.id, nextQuantity(item.quantity, -1)));
  card.append(title, button);
  return card;
}

export function compactProductCard(product, onAdd) {
  const card = document.createElement('article');
  card.className = 'card card--compact';
  const title = document.createElement('h2');
  title.textContent = product.title;
  const button = document.createElement('button');
  button.textContent = 'Add';
  button.addEventListener('click', () => onAdd(product.id));
  card.append(title, button);
  return card;
}
