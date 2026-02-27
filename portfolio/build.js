const fs = require('fs');

const GITHUB_USER = 'guilherme994';
const GITHUB_TOKEN = process.env.GITHUB_TOKEN;

async function fetchPinnedRepos() {
  const query = `
    query {
      user(login: "${GITHUB_USER}") {
        pinnedItems(first: 3, types: REPOSITORY) {
          nodes {
            ... on Repository {
              name
              description
              url
              homepageUrl
            }
          }
        }
      }
    }
  `;

  const response = await fetch('https://api.github.com/graphql', {
    method: 'POST',
    headers: {
      'Authorization': `Bearer ${GITHUB_TOKEN}`,
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({ query }),
  });

  const { data } = await response.json();
  return data.user.pinnedItems.nodes;
}

function buildProjectsHtml(repos) {
  return repos.map((repo, index) => {
    const demo = repo.homepageUrl
      ? `<a class="chip" href="${repo.homepageUrl}" target="_blank" rel="noreferrer">Demo</a>`
      : '';
   return `          <article class="item">
            <div>
              <a href="${repo.url}" target="_blank" rel="noreferrer"><h3>${repo.name}</h3></a>
              <a href="${repo.url}" target="_blank" rel="noreferrer"><p>${repo.description ?? 'Sem descrição.'}</p></a>
            </div>
            <div class="links">
              <a class="chip" href="${repo.url}" target="_blank" rel="noreferrer">Código</a>
              ${demo}
            </div>
          </article>`;
  }).join('\n');
}

async function build() {
  if (!GITHUB_TOKEN) {
    console.error('Erro: variável GITHUB_TOKEN não definida.');
    process.exit(1);
  }

  console.log('Buscando repositórios pinados...');
  const repos = await fetchPinnedRepos();

  const projectsHtml = buildProjectsHtml(repos);

  let html = fs.readFileSync('./site/index.html', 'utf-8');

  html = html.replace(
    /<!-- PROJECTS:START -->[\s\S]*?<!-- PROJECTS:END -->/,
    `<!-- PROJECTS:START -->\n${projectsHtml}\n          <!-- PROJECTS:END -->`
  );

  fs.writeFileSync('./site/index.html', html);
  console.log(`Pronto. ${repos.length} projetos inseridos.`);
}

build().catch(err => {
  console.error('Erro durante o build:', err);
  process.exit(1);
});
