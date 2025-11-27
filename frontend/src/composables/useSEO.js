import { useTitle } from '@vueuse/core'

export function useSEO(title, description, image = null, jsonLd = null) {
    // Update Title
    const pageTitle = useTitle()
    pageTitle.value = `${title} | Zsdevweb`

    // Update Meta Description
    updateMeta('description', description || 'Solutions web innovantes et sur mesure.')

    // Update OG Tags
    updateMeta('og:title', `${title} | Zsdevweb`, 'property')
    updateMeta('og:description', description || 'Solutions web innovantes et sur mesure.', 'property')
    if (image) {
        updateMeta('og:image', image, 'property')
    }

    // Update Twitter Tags
    updateMeta('twitter:title', `${title} | Zsdevweb`, 'property')
    updateMeta('twitter:description', description || 'Solutions web innovantes et sur mesure.', 'property')
    if (image) {
        updateMeta('twitter:image', image, 'property')
    }

    // Update Canonical URL
    const canonicalUrl = window.location.href
    let link = document.querySelector('link[rel="canonical"]')
    if (!link) {
        link = document.createElement('link')
        link.setAttribute('rel', 'canonical')
        document.head.appendChild(link)
    }
    link.setAttribute('href', canonicalUrl)

    // Inject JSON-LD
    if (jsonLd) {
        let script = document.querySelector('script[type="application/ld+json"]')
        if (!script) {
            script = document.createElement('script')
            script.setAttribute('type', 'application/ld+json')
            document.head.appendChild(script)
        }
        script.textContent = JSON.stringify(jsonLd)
    }
}

function updateMeta(name, content, attribute = 'name') {
    let meta = document.querySelector(`meta[${attribute}="${name}"]`)
    if (!meta) {
        meta = document.createElement('meta')
        meta.setAttribute(attribute, name)
        document.head.appendChild(meta)
    }
    meta.setAttribute('content', content)
}
