export const ORG_COLORS: Record<string, string> = {
  'OpenAI': '#74aa9c',
  'Anthropic': '#d4a574',
  'Google': '#4285f4',
  'Meta': '#0668e1',
  'Mistral AI': '#ff7000',
  'DeepSeek': '#4a90d9',
  'Alibaba': '#ff6a00',
};

export function orgColor(org: string): string {
  return ORG_COLORS[org] || '#6366F1';
}
