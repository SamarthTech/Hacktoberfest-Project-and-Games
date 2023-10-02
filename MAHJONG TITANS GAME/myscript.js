let cells;
let colors;
let table;
let counter;
let selectedCell;

let tableWidth;
let tableHeight;

let correctMoves;
let wrongMoves;

let totalTime;
let count;

/**
 * Shuffle the given array
 *
 * @param {array} arr         The array to shuffle
 * @return {array}            The array shuffled
 */
const shuffle = (arr) => {
  let currentIndex = arr.length;
  let temporaryValue;
  let randomIndex;

  // While there remain elements to shuffle...
  while (currentIndex !== 0) {
    // Pick a remaining element...
    randomIndex = Math.floor(Math.random() * currentIndex);
    currentIndex -= 1;

    // And swap it with the current element.
    temporaryValue = arr[currentIndex];
    arr[currentIndex] = arr[randomIndex];
    arr[randomIndex] = temporaryValue;
  }

  return arr;
};

/**
 * Hide a cell so it is not visible
 *
 * @param {number} cellId     The id of the cell to hide
 */
const hideCell = (cellId) => {
  cells[cellId].setAttribute('cell-status', 'deactivated');

  if (cells[cellId].innerHTML === '-1') {
    cells[cellId].style.display = 'none';
  } else {
    cells[cellId].className = 'cell-disappear-animation gameTable cellGradient';
  }
};

/**
 * Check if the cell with the given id is active
 *
 * @param {number} cellId     The id of the cell to check
 * @return {boolean}          Whether the cell with the given id is active or not
 */
const cellIsActive = (cellId) => cells[cellId].getAttribute('cell-status') !== 'deactivated';

/**
 * Check if there is no active cell on the left of the cell with the given id
 * (or if it's on the left side of the board)
 *
 * @param {number} cellId     The id of the cell to check
 * @return {boolean}          Whether the cell on the left is free or not
 */
const isFreeLeft = (cellId) => cellId % tableWidth === 0 || !cellIsActive(cellId - 1);

/**
 * Check if there is noa ctive cell on the right of the cell with the given id
 * (or if it's on the right side of the board)
 *
 * @param {number} cellId     The id of the cell to check
 * @return {boolean}          Whether the cell on the right is free or not
 */
const isFreeRight = (cellId) => cellId % tableWidth === tableWidth - 1 || !cellIsActive(cellId + 1);

/**
 * Check if the cell with the given id can be removed
 * (according to mahjong rules)
 *
 * @param {number} cellId     The id of the cell to check
 * @return {boolean}          Whether the cell with the given id can be removed or not
 */
const canBeRemoved = (cellId) => isFreeLeft(cellId) || isFreeRight(cellId);

/**
 * Make a cell selected
 *
 * @param {number} cellId     The id of the cell to select
 */
const makeSelected = (cellId) => {
  cells[cellId].className = 'gameTable selectedCellGradient';
  selectedCell = cellId;
};

/**
 * Make a cell the default color (unselected)
 *
 * @param {number} cellId     The id of the cell to deselect
 */
const makeDeselected = (cellId) => {
  cells[cellId].className = 'gameTable cellGradient';
};

/**
 * Update move counters UI
 */
const updateMoveCounters = () => {
  document.getElementById('correctMovesCounter').innerHTML = `Valid moves: <span style="color:green">${correctMoves}</span> | `;
  document.getElementById('wrongMovesCounter').innerHTML = `Invalid moves: <span style="color:red">${wrongMoves}</span> | `;
};

/**
 * Count a correct or wrong move
 *
 * @param {string} wat        Whether the move was 'correct' or 'wrong'
 */
const countMove = (wat) => {
  if (wat === 'correct') {
    correctMoves += 1;
  } else if (wat === 'wrong') {
    wrongMoves += 1;
  }

  updateMoveCounters();
};

/**
 * Remove stuff from page and tell user if they won
 *
 * @param {boolean} win       Whether the user has won or not
 */
const endGame = (win) => {
  document.getElementById('theTable').parentNode.removeChild(document.getElementById('theTable'));
  document.getElementById('bottomBar').parentNode.removeChild(document.getElementById('bottomBar'));

  const totalMoves = correctMoves + wrongMoves;

  let correctPercentage = 0;
  let wrongPercentage = 0;

  if (totalMoves !== 0) {   // to prevent division by 0
    correctPercentage = (correctMoves / totalMoves) * 100;
    wrongPercentage = 100 - correctPercentage;

    // Round to 2 decimal places
    correctPercentage = +correctPercentage.toFixed(2);
    wrongPercentage = +wrongPercentage.toFixed(2);
  }

  let message = (win) ? 'You win :D\n' : 'You lose! :(\n';
  message += `\nTotal time: ${totalTime - count} seconds\nValid moves: ${correctPercentage}%\nInvalid moves: ${wrongPercentage}%`;

  // eslint-disable-next-line no-alert
  alert(message);

  window.location = 'index.html';
};

/**
 * Checks if the row with the given id has any active cells
 *
 * @param {number} rowId      The id of the row to check
 * @return {boolean}          `true` if it has at least one,
 *                            `false` otherwise
 */
const rowHasActiveCell = (rowId) => {
  const row = table.rows[rowId].cells;

  for (let i = 0; i < row.length; i += 1) {
    if (cellIsActive(row[i].id)) {
      return true;
    }
  }

  return false;
};

/**
 * Check if the board is empty
 *
 * @return {boolean}          Whether the board is empty or not
 */
const boardEmpty = () => {
  for (let i = 0; i < tableHeight; i += 1) {
    if (rowHasActiveCell(i)) {
      return false;
    }
  }

  return true;
};

/**
 * Return the id of the leftmost active cell of the row with the given id
 *
 * @param {number} rowId      The id of the row to check
 * @return {number}           The id of the leftmost active cell of the row
 */
const getLeft = (rowId) => {
  const row = table.rows[rowId].cells;

  for (let i = 0; i < row.length; i += 1) {
    if (cellIsActive(row[i].id)) {
      return row[i].id;
    }
  }
};

/* Return the id of the RIGHT_MOST ACTIVE CELL OF THE ROW WITH ID rowId */
const getRight = (rowId) => {
  const row = table.rows[rowId].cells;

  for (let i = row.length; i > 0; i -= 1) {
    if (cellIsActive(row[i - 1].id)) {
      return row[i - 1].id;
    }
  }
};

/**
 * Count how many tiles are available (= can be moved) with the given number in them
 *
 * @param {number} num        The number to check
 * @return {number}           The number of tiles that are available with the given number in them
 */
const countAvailable = (num) => {
  let counter = 0;
  const numOfRows = table.rows.length;

  for (let i = 0; i < numOfRows; i += 1) {
    if (rowHasActiveCell(i)) {
      const leftCellId = getLeft(i);
      const rightCellId = getRight(i);

      // eslint-disable-next-line eqeqeq
      if (cells[leftCellId].innerHTML == num) {
        counter += 1;
      }

      // eslint-disable-next-line eqeqeq
      if (cells[rightCellId].innerHTML == num && rightCellId !== leftCellId) {
        counter += 1;
      }
    }
  }

  return counter;
};

/**
 * Check if there are no moves available
 * If it's `true`, the board should be shuffled
 *
 * @return {boolean}          Whether it is stuck or not
 */
const isStuck = () => {
  const numOfRows = table.rows.length;

  for (let i = 0; i < numOfRows; i += 1) {
    if (rowHasActiveCell(i)) {
      if (countAvailable(cells[getLeft(i)].innerHTML) > 1) {
        // console.log(`More than one cells with ${cells[getLeft(i)].innerHTML} can be removed`);
        return false;
      }

      if (countAvailable(cells[getRight(i)].innerHTML) > 1) {
        // console.log(`More than one cells with ${cells[getRight(i)].innerHTML} can be removed`);
        return false;
      }
    }
  }

  return true;
};

/* Generate a random color
 *
 * @return {string}           A random hex color
 */
const getRandomColor = () => {
  const letters = '0123456789ABCDEF'.split('');
  let color = '#';

  for (let i = 0; i < 6; i += 1) {
    color += letters[Math.round(Math.random() * 15)];
  }

  return color;
};

/**
 * Initialize the `colors` global array with colors to use for each number
 *
 * @param {number} limit      The maximum number (and size of array)
 */
const makeGlobalColorsArray = (limit) => {
  colors = [];

  for (let i = 0; i < limit; i += 1) {
    colors.push(getRandomColor());
  }
};

/**
 * Add a cell at the end of a row
 *
 * @param {HTMLTableRowElement} row
 * @param {string} innerHTL
 * @param {number} counter
 */
const addCell = (row, innerHTML, counter) => {
  const col = row.insertCell(row.childElementCount);
  col.innerHTML = innerHTML;
  cells[counter] = col;
  col.id = counter;
  col.style.opacity = 0;
  col.style.border = `2px solid ${colors[innerHTML]}`;
  col.setAttribute('class', 'gameTable');
  col.setAttribute('onclick', `cellPressed(${counter});`);
  col.setAttribute('onmouseover', `mouseOver(${counter});`);
  col.setAttribute('onmouseout', `mouseOut(${counter});`);
  col.setAttribute('cell-status', 'active');    // for checking if cell is active

  if (innerHTML === -1) {                       // for hiding cells when shuffling board
    hideCell(counter);
  }
};

/**
 * Add rows and cells to the table
 *
 * @param {array} cellNumbers   An array containing the cell numbers of the table to create
 */
const createTable = (cellNumbers) => {
  cells = new Array(tableHeight * tableWidth);
  let counter = 0;

  for (let i = 0; i < tableHeight; i += 1) {
    const row = table.insertRow(i);
    row.setAttribute('class', 'gameTable');
    for (let j = 0; j < tableWidth; j += 1) {
      addCell(row, cellNumbers[counter], counter);
      counter += 1;
    }
  }
};

/**
 * Animate the table
 *
 * @param {number} i
 */
const animateTable = (i) => {
  cells[i].style.opacity = 1;
  cells[i].className = 'cell-move-in-animation gameTable cellGradient';

  if (i > 0) {
    setTimeout(animateTable, 10, i - 1);
  }
};

/**
 * Shuffle the board
 */
const shuffleBoard = () => {
  let activeCellNumbers = [];

  // Copy active cells to new array
  for (let i = 0; i < cells.length; i += 1) {
    if (cellIsActive(i)) {
      activeCellNumbers.push(cells[i].innerHTML);
    }
  }

  // Shuffle new array
  activeCellNumbers = shuffle(activeCellNumbers);

  const numOfCellsToAnimate = activeCellNumbers.length;

  // Add -1 to empty spaces of new array
  for (let i = activeCellNumbers.length; i < cells.length; i += 1) {
    activeCellNumbers.push(-1);
  }

  // Delete rows from current table (to add new ones)
  while (table.rows.length > 0) {
    table.deleteRow(0);
  }

  // Add new table with new cells
  createTable(activeCellNumbers);

  selectedCell = -1;  // resetting this, no cells are selected after shuffling le board

  if (isStuck()) {
    shuffleBoard();
  }

  animateTable(numOfCellsToAnimate - 1);
};

/**
 * Handle cell clicks
 *
 * @param {number} cellId     The id of the cell that was clicked
 */
const cellPressed = (cellId) => {
  if (cellIsActive(cellId)) {
    if (cellId !== selectedCell && selectedCell !== -1) {
      // Check if the selected cell can be removed, and highlight it or do nothing
      if (canBeRemoved(cellId)) {
        if (cells[selectedCell].innerHTML === cells[cellId].innerHTML) {
          // User found a match, hide cells!
          hideCell(selectedCell);
          hideCell(cellId);
          selectedCell = -1;

          countMove('correct');

          if (boardEmpty()) {               // checking if user has won the game
            endGame(true);
            return;
          }

          if (isStuck()) {                  // because cells changed, must check if game is stuck
            shuffleBoard();
          }
        } else {                            // selected 2 cells with different values, so wrong move
          makeDeselected(selectedCell);     // change previously selected cell to default color
          makeSelected(cellId);             // select the clicked cell!
          countMove('wrong');
        }
      } else {                              // clicked a cell that cannot be removed, so wrong move
        makeDeselected(selectedCell);       // deselect the selected cell
        selectedCell = -1;
        countMove('wrong');
      }
    } else if (cellId === selectedCell) {   // clicked on the same cell twice, deselecting it
      makeDeselected(cellId);               // (does not count as a wrong move)
      selectedCell = -1;
    } else if (canBeRemoved(cellId)) {      // there is no selected cell, selecting the clicked one
      makeSelected(cellId);
    }
  }
};

/**
 * Change the appearance of a cell on mouse over
 *
 * @param {number} cellId       The id of the cell to change its appearance
 */
const mouseOver = (cellId) => {
  if (cellId !== selectedCell && cellIsActive(cellId) && canBeRemoved(cellId)) {
    cells[cellId].className = 'gameTable mouseOverCellGradient';
  }
};

/**
 * Change the appearance of a cell on mouse out
 *
 * @param {number} cellId       The id of the cell to change its appearance
 */
const mouseOut = (cellId) => {
  if (cellId !== selectedCell && cellIsActive(cellId) && canBeRemoved(cellId)) {
    cells[cellId].className = 'gameTable cellGradient';
  }
};

const gimmeTitle = () => {
  document.getElementById('title').innerHTML = '&#3900;&#32;&#12388;&#32;&#9685;&#95;&#9685;&#32;&#3901;&#12388; MAHJONG TITANS';
  setTimeout(() => {
    document.getElementById('title').innerHTML = 'MAHJONG TITANS';
  }, 500);
};

/**
 * Make a randomized array for the game with the defined dimensions and difficulty
 *
 * @param {number} leWidth        The table width
 * @param {number} leHeight       The table height
 * @param {number} difficulty     The difficulty
 * @return {array}                The randomized array for the game
 */
const makeMahjongArray = (leWidth, leHeight, difficulty) => {
  const numbers = new Array(leWidth * leHeight);
  const limit = numbers.length / (2 ** difficulty);     // 8, 4 or 2

  const iLoops = 2 ** difficulty;
  for (let i = 0; i < iLoops; i += 1) {
    for (let j = 0; j < limit; j += 1) {
      numbers[(i * limit) + j] = j;
    }
  }

  return shuffle(numbers);
};

/**
 * Create "New Game" button
 */
const createNewGameButton = () => {
  const button = document.createElement('input');
  button.type = 'button';
  button.value = 'NEW GAME';
  button.onclick = () => {
    window.location = 'index.html';
  };
  document.getElementById('nGButton').appendChild(button);
};

/**
 * Add the timer that counts the time, on the bottom bar :D
 */
const addTimerToBottomBar = () => {
  document.getElementById('timeCounter').innerHTML = `${count} seconds`;
};

/* Function to initialize move counters */
const initMoveCounters = () => {
  wrongMoves = 0;
  correctMoves = 0;
  updateMoveCounters();
};

/**
 * Countdown timer
 */
const timer = () => {
  count -= 1;

  // If time is up, user lost the game
  if (count <= 0) {
    clearInterval(counter);
    endGame(false);
    return;
  }

  // If user didn't lose the game
  document.getElementById('timeCounter').innerHTML = `${count}${(count === 1) ? ' second' : ' seconds'}`;
  if (count === 10) {
    document.getElementsByTagName('body')[0].className = 'timeIsUp-animation';
  }
};

/**
 * Start counting down until game over
 */
const initTimer = () => {
  totalTime = 300;          // 300 seconds = 5 minutes
  count = totalTime;
  counter = setInterval(timer, 1000);

  addTimerToBottomBar();
};

/**
 * Call the functions that add things to the bottom bar
 * (below the mahjong board)
 */
const addThingsToBottomBar = () => {
  createNewGameButton();
  initTimer();
  initMoveCounters();
  document.getElementById('bottomBar').className = 'bottomBar-animation';
};

/**
 * Start the game
 */
const startGame = () => {
  // Get variables from html page
  const size = document.getElementById('sizeSlider').value;

  // Subtract from 4, so 3 is hardest, 1 is easiest (the opposite of the slider's value)
  const difficulty = 4 - document.getElementById('difficultySlider').value;

  // Remove settings
  const div = document.getElementById('startscreenDiv');
  div.parentNode.removeChild(div);

  // Create the table
  table = document.createElement('table');  // global variable
  table.setAttribute('class', 'gameTable');
  table.id = 'theTable';

  tableHeight = 2 * size;
  tableWidth = 4 * size;

  const numbers = makeMahjongArray(tableWidth, tableHeight, difficulty);
  makeGlobalColorsArray(numbers.length / (2 ** difficulty));

  createTable(numbers);    // the function also creates the global array cells

  selectedCell = -1;       // global variable with selected cell

  // Shuffle the board if there are no moves to make
  if (isStuck()) {
    shuffleBoard();
  }

  // Add the table to the page
  document.getElementById('divTable').appendChild(table);

  animateTable(cells.length - 1);

  // Add the new game button and other things to the bottom bar
  addThingsToBottomBar();
};
