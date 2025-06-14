export function initListView(config) {
  const {
    listElId,
    apiUrl,
    rowBuilder,
    sortButtons = {},
    tagFilterSelector = null,
    defaultOrdering = '',
    scope = null,
  } = config;

  const listEl = document.getElementById(listElId);
  const prevBtn = document.getElementById('prev-page');
  const nextBtn = document.getElementById('next-page');

  let currentPage = 1;
  const pageSize = 5;
  let ordering = defaultOrdering;

  function updatePaginationButtons(totalCount) {
    const maxPage = Math.ceil(totalCount / pageSize);
    prevBtn.disabled = currentPage <= 1;
    nextBtn.disabled = currentPage >= maxPage;
  }

  function getTagFilterValues() {
    if (!tagFilterSelector) return [];
    return [...document.querySelectorAll(tagFilterSelector)]
      .filter(i => i.checked)
      .map(i => i.value);
  }

  function loadList() {
    const params = new URLSearchParams();
    if (ordering) params.append('ordering', ordering);
    if (scope) params.append('scope', scope);
    params.append('limit', pageSize);
    params.append('offset', (currentPage - 1) * pageSize);

    getTagFilterValues().forEach(id => params.append('tagi', id));

    fetch(`${apiUrl}?${params.toString()}`, {
      headers: { 'Accept': 'application/json' }
    })
      .then(r => r.json())
      .then(data => {
        listEl.innerHTML = '';
        const results = data.results || [];
        if (results.length === 0) {
          listEl.innerHTML = '<tr><td colspan="10">Brak danych.</td></tr>';
          updatePaginationButtons(0);
          return;
        }

        results.forEach(obj => {
          const row = rowBuilder(obj);
          listEl.appendChild(row);
        });

        updatePaginationButtons(data.count);
      });
  }

  // Sorting buttons
  for (const [buttonId, sortValue] of Object.entries(sortButtons)) {
    const btn = document.getElementById(buttonId);
    if (btn) {
      btn.onclick = () => {
        ordering = sortValue;
        currentPage = 1;
        loadList();
      };
    }
  }

  // Tag filtering
  if (tagFilterSelector) {
    document.querySelectorAll(tagFilterSelector).forEach(cb => {
      cb.onchange = () => {
        currentPage = 1;
        loadList();
      };
    });
  }

  // Pagination
  prevBtn.onclick = () => {
    if (currentPage > 1) {
      currentPage--;
      loadList();
    }
  };

  nextBtn.onclick = () => {
    currentPage++;
    loadList();
  };

  window.addEventListener('DOMContentLoaded', loadList);
}
