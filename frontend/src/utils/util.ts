export function findPageNumber(
  maxPages: number,
  currentPageNo: number,
  amountShown: number = 3
) {
  // Determine range of numbers to include in navigation bar
  let sp = currentPageNo;
  let ep = currentPageNo;
  while (ep - sp + 1 < amountShown) {
    if (sp - 1 <= 0 && ep + 1 > maxPages) break;

    if (sp - 1 > 0) sp -= 1;

    if (ep + 1 <= maxPages) ep += 1;
  }

  let ret = [];
  for (let i = sp; i <= ep; i++) {
    ret.push(i);
  }
  return ret;
}
