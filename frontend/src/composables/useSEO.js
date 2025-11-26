import { useTitle } from '@vueuse/core'

export function useSEO(title, description) {
    // Update Title
    const pageTitle = useTitle()
    pageTitle.value = `${title} | Zsdevweb`

    // Update Meta Description
    const metaDescription = document.querySelector('meta[name="description"]')
    if (metaDescription) {
        metaDescription.setAttribute('content', description || 'Solutions web innovantes et sur mesure.')
    }

    // Update OG Title
    const ogTitle = document.querySelector('meta[property="og:title"]')
    if (ogTitle) {
        ogTitle.setAttribute('content', `${title} | Zsdevweb`)
    }

    // Update OG Description
    const ogDescription = document.querySelector('meta[property="og:description"]')
    if (ogDescription) {
        ogDescription.setAttribute('content', description || 'Solutions web innovantes et sur mesure.')
    }
}
